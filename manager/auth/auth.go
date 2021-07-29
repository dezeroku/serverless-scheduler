package auth

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"net/http"
	"net/url"
	"os"
	"regexp"
	"strings"
	"text/template"
	"time"

	"github.com/d0ku/monitor-page/manager/v2/common"
	"github.com/golang-jwt/jwt"
	"github.com/gorilla/mux"
	"github.com/jinzhu/gorm"
	uuid "github.com/nu7hatch/gouuid"
)

var config struct {
	appURL    *url.URL
	jwtKey    []byte
	senderAPI string
}

var (
	rxEmail = regexp.MustCompile("^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$")
)
var magicLinkTmpl = template.Must(template.ParseFiles("templates/magic-link.html"))
var db *gorm.DB

type ContextKey struct {
	Name string
}

type User struct {
	Email             string `gorm:"primary_key" json:"email"`
	VerificationCodes []VerificationCode
}

type VerificationCode struct {
	gorm.Model
	Code      string `gorm:"primary_key"`
	UserEmail string `gorm:"not null"`
	Timeout   int64  `gorm:"not null"`
}

var KeyAuthUserEmail = ContextKey{"auth_user_email"}

func withAuth(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		a := r.Header.Get("Authorization")
		hasToken := strings.HasPrefix(a, "Bearer ")
		if !hasToken {
			next(w, r)
			return
		}

		tokenString := a[7:]

		p := jwt.Parser{ValidMethods: []string{jwt.SigningMethodHS256.Name}}
		token, err := p.ParseWithClaims(
			tokenString,
			&jwt.StandardClaims{},
			func(*jwt.Token) (interface{}, error) { return config.jwtKey, nil },
		)
		if err != nil {
			http.Error(w, http.StatusText(http.StatusUnauthorized), http.StatusUnauthorized)
			return
		}

		claims, ok := token.Claims.(*jwt.StandardClaims)
		if !ok || !token.Valid {
			http.Error(w, http.StatusText(http.StatusUnauthorized), http.StatusUnauthorized)
			return
		}

		ctx := r.Context()
		ctx = context.WithValue(ctx, KeyAuthUserEmail, claims.Subject)

		next(w, r.WithContext(ctx))
	}
}

// Authentication provides Middleware to authenticate using JWT obtained by passwordless.
type Authentication struct{}

// Middleware provides checking for JWT token and its correctness.
func (a *Authentication) Middleware(next http.Handler) http.Handler {
	return withAuth(func(w http.ResponseWriter, r *http.Request) {
		_, ok := r.Context().Value(KeyAuthUserEmail).(string)
		if !ok {
			http.Error(w, http.StatusText(http.StatusUnauthorized), http.StatusUnauthorized)
			return
		}
		next.ServeHTTP(w, r)
	})
}

func passwordlessStart(w http.ResponseWriter, r *http.Request) {
	var input struct {
		Email       string `json:"email"`
		RedirectURI string `json:"redirectUri"`
	}
	if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	defer r.Body.Close()

	errs := make(map[string]string)
	if input.Email == "" {
		errs["email"] = "Email required"
	} else if !rxEmail.MatchString(input.Email) {
		errs["email"] = "Invalid email"
	}
	if input.RedirectURI == "" {
		errs["redirectUri"] = "Redirect URI required"
	} else if u, err := url.Parse(input.RedirectURI); err != nil || !u.IsAbs() {
		errs["redirectUri"] = "Invalid redirect URI"
	}
	if len(errs) != 0 {
		common.RespondJSON(w, errs, http.StatusUnprocessableEntity)
		return
	}

	var user User
	if db.First(&user, "email = ?", input.Email).RecordNotFound() {
		log.Printf("No user with such mail: %s\n", input.Email)
		w.WriteHeader(http.StatusNoContent)
		return
	}
	temp, err := uuid.NewV4()
	if err != nil {
		log.Println("Could not generate UUID.")
		return
	}
	u := temp.String()
	fmt.Println(u)

	// Check whether last verification code was sent at least 15 minutes before current one.
	var lastCode VerificationCode
	lastCodeFound := !db.Last(&lastCode, "user_email = ?", input.Email).RecordNotFound()

	if lastCodeFound {
		if lastCode.CreatedAt.After(time.Now().Add(-1 * time.Minute * 15)) {
			log.Printf("Request another verification code before cooldown: %s\n", input.Email)
			w.WriteHeader(http.StatusTooManyRequests)
			return
		}
	}

	verificationCode := &VerificationCode{Code: u, UserEmail: input.Email, Timeout: time.Now().Add(time.Minute * 15).Unix()}
	db.Create(verificationCode)

	q := make(url.Values)
	q.Set("verification_code", verificationCode.Code)
	q.Set("redirect_uri", input.RedirectURI)
	magicLink := *config.appURL
	magicLink.Path = "/passwordless/verify_redirect"
	magicLink.RawQuery = q.Encode()

	var body bytes.Buffer
	data := map[string]string{"MagicLink": magicLink.String()}
	if err := magicLinkTmpl.Execute(&body, data); err != nil {
		common.RespondInternalError(w, fmt.Errorf("could not execute magic link template: %v", err))
		return
	}

	if err := sendMail(input.Email, "Magic Link", body.String()); err != nil {
		log.Printf("could not mail magic link to %s: %v\n", input.Email, err)
		http.Error(w, "Could not mail your magic link. Try again later", http.StatusServiceUnavailable)
		return
	}

	w.WriteHeader(http.StatusNoContent)
}

type mail struct {
	Recipients  []string  `json:"recipients"`
	HTMLContent string    `json:"html_content"`
	Subject     string    `json:"subject"`
	Data        *mailData `json:"data"`
}

type mailData struct {
	Url         string        `json:"url"`
	Attachments []*attachment `json:"attachments"`
}

type attachment struct {
	Filename string `json:"filename"`
	Content  string `json:"content"`
	Filetype string `json:"filetype"`
}

func sendMail(to, subject, body string) error {
	_, ok := os.LookupEnv("DEVELOP_MODE")
	if ok {
		fmt.Println("SEND ME!")
		fmt.Println(body)
		fmt.Println("NOT SENDING MAIL")
		return nil
	}

	fmt.Println(config.senderAPI)
	emptySlice := make([]*attachment, 0)
	dataObject := &mailData{Url: "does not really matter", Attachments: emptySlice}
	recipients := make([]string, 0)
	recipients = append(recipients, to)
	mailObject := &mail{Recipients: recipients, HTMLContent: body, Subject: subject, Data: dataObject}
	val, _ := json.Marshal(mailObject)
	req, _ := http.NewRequest("POST", config.senderAPI+"/v1/mail", bytes.NewBuffer(val))
	req.Header.Set("Content-Type", "application/json")
	req.Body.Close()
	client := &http.Client{}
	res, e := client.Do(req)
	if e != nil {
		return e
	}

	defer res.Body.Close()

	fmt.Println("response Status:", res.Status)
	if res.StatusCode != http.StatusOK {
		log.Printf("Incorrect http status: %d (%s)\n", res.StatusCode, res.Status)
		return errors.New("Incorrect http status")
	}
	return nil
}

func passwordlessVerifyRedirect(w http.ResponseWriter, r *http.Request) {
	q := r.URL.Query()
	verificationCode := q.Get("verification_code")
	redirectURI := q.Get("redirect_uri")
	errs := make(map[string]string)
	if verificationCode == "" {
		errs["verification_code"] = "Verification code required"
	} else {
		_, err := uuid.ParseHex(verificationCode)
		if err != nil {
			errs["verification_code"] = "Invalid verification code"
		}
	}
	var callback *url.URL
	var err error
	if redirectURI == "" {
		errs["redirect_uri"] = "Redirect URI required"
	} else if callback, err = url.Parse(redirectURI); err != nil || !callback.IsAbs() {
		errs["redirect_uri"] = "Invalid redirect URI"
	}
	if len(errs) != 0 {
		common.RespondJSON(w, errs, http.StatusUnprocessableEntity)
		return
	}
	var user User
	code := &VerificationCode{Code: verificationCode}
	notExists := db.First(&code, "code = ?", verificationCode).RecordNotFound()
	if notExists {
		http.Error(w, "Link already used or incorrect", http.StatusBadRequest)
		return
	}
	err = db.Delete(&code).Error

	if code.Timeout < time.Now().Unix() {
		http.Error(w, "Link expired", http.StatusBadRequest)
		return
	}

	if err != nil {
		http.Error(w, "Could not delete code", http.StatusBadRequest)
	}
	db.First(&user, "email = ?", code.UserEmail)
	expiresAt := time.Now().Add(time.Hour * 2)
	tokenString, err := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.StandardClaims{
		Subject:   user.Email,
		ExpiresAt: expiresAt.Unix(),
	}).SignedString(config.jwtKey)
	if err != nil {
		common.RespondInternalError(w, fmt.Errorf("could not create JWT: %v", err))
		return
	}
	expiresAtB, err := expiresAt.MarshalText()
	if err != nil {
		common.RespondInternalError(w, fmt.Errorf("could not marshal expiration date: %v", err))
		return
	}
	f := make(url.Values)
	f.Set("jwt", tokenString)
	f.Set("expires_at", string(expiresAtB))
	callback.Fragment = f.Encode()
	http.Redirect(w, r, callback.String(), http.StatusFound)
}

// NewRouter returns gorilla/mux router wih already initialized subrouter for authentication.
// It should probably be available under /passwordless
// Provides endpoints:
//     /start
//     /verify_redirect
func NewRouter(appURL string, jwtKey string, senderAPI string, dbIn *gorm.DB) *mux.Router {
	config.appURL, _ = url.Parse(appURL)
	config.jwtKey = []byte(jwtKey)
	config.senderAPI = senderAPI

	db = dbIn
	// Migrate the schema
	db.AutoMigrate(&VerificationCode{})
	db.AutoMigrate(&User{})

	_, ok := os.LookupEnv("DEVELOP_MODE")
	if ok {
		log.Println("Inserting dummy users to DB.")
		db.Save(&User{Email: "d0ku@example.url"})
		db.Save(&User{Email: "test@example.url"})
	}

	router := mux.NewRouter()

	router.HandleFunc("/start", common.RequireJSON(passwordlessStart)).Methods("POST")
	router.HandleFunc("/verify_redirect", passwordlessVerifyRedirect).Methods("GET")

	return router
}
