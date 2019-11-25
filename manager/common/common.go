package common

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"strings"
)

func Env(key, fallbackValue string) string {
	v, ok := os.LookupEnv(key)
	if !ok {
		return fallbackValue
	}
	return v
}

func RequireJSON(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		if ct := r.Header.Get("Content-Type"); !strings.HasPrefix(ct, "application/json") {
			http.Error(w, "Content type of application/json required", http.StatusUnsupportedMediaType)
			return
		}
		next(w, r)
	}
}

func RespondJSON(w http.ResponseWriter, payload interface{}, code int) {
	b, err := json.Marshal(payload)
	if err != nil {
		RespondInternalError(w, fmt.Errorf("could not marshal response payload: %v", err))
		return
	}
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.WriteHeader(code)
	w.Write(b)
}

func RespondInternalError(w http.ResponseWriter, err error) {
	log.Println(err)
	http.Error(w,
		http.StatusText(http.StatusInternalServerError),
		http.StatusInternalServerError)
}
