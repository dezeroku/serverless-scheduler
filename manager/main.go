package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"strings"

	"github.com/d0ku/monitor_page/manager/v2/auth"
	"github.com/d0ku/monitor_page/manager/v2/swagger"
	"github.com/gorilla/handlers"
	"github.com/gorilla/mux"
	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/postgres"
	_ "github.com/jinzhu/gorm/dialects/sqlite"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"
)

func testResponse(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("Everything is good!"))
	ctx := r.Context()
	authUserEmail := ctx.Value(auth.KeyAuthUserEmail)
	fmt.Println(authUserEmail)
}

func mount(r *mux.Router, path string, handler http.Handler) {
	r.PathPrefix(path).Handler(
		http.StripPrefix(
			strings.TrimSuffix(path, "/"),
			handler,
		),
	)
}

func main() {
	var err error
	var db *gorm.DB
	_, ok := os.LookupEnv("DEVELOP_MODE")
	if ok {
		db, err = gorm.Open("sqlite3", "test.db")
		log.Println("No DATABASE_URL in environment, using sqlite3.")
	} else {
		databaseType, ok := os.LookupEnv("DATABASE_TYPE")
		if !ok {
			panic("No DATABASE_TYPE provided.")
		}

		if databaseType != "sqlite3" {
			log.Println("Non-sqlite3 DB used")
			databaseUser, ok := os.LookupEnv("DATABASE_USER")
			if !ok {
				panic("No DATABASE_USER provided.")
			}
			databasePassword, ok := os.LookupEnv("DATABASE_PASSWORD")
			if !ok {
				panic("No DATABASE_PASSWORD provided.")
			}
			databasePort, ok := os.LookupEnv("DATABASE_PORT")
			if !ok {
				panic("No DATABASE_PORT provided.")
			}
			databaseHost, ok := os.LookupEnv("DATABASE_HOST")
			if !ok {
				panic("No DATABASE_HOST provided.")
			}
			databaseDBName, ok := os.LookupEnv("DATABASE_DB_NAME")
			if !ok {
				panic("No DATABASE_DB_NAME provided.")
			}

			databaseConnString := fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=require", databaseHost, databasePort, databaseUser, databasePassword, databaseDBName)

			db, err = gorm.Open(databaseType, databaseConnString)

		} else {
			log.Println("sqlite3 DB used")

			databaseLocation, ok := os.LookupEnv("DATABASE_LOCATION")
			if !ok {
				panic("No DATABASE_LOCATION provided.")
			}
			db, err = gorm.Open("sqlite3", databaseLocation)
		}
	}

	if err != nil {
		panic("failed to connect database")
	}

	defer db.Close()

	helper := func(name string) string {
		temp, ok := os.LookupEnv(name)
		if !ok {
			log.Fatalln("could not find " + name + " in environment variables")
		}
		return temp
	}

	jwtKey := helper("JWT_KEY")

	appURL := helper("APP_URL")

	helperConfig := func(name string, m map[string]string) {
		t := helper(name)
		m[name] = t
	}

	checkerConfig := make(map[string]string)

	helperConfig("SENDER_API_PORT", checkerConfig)
	helperConfig("SENDER_SERVICE", checkerConfig)

	helperConfig("CHECKER_IMAGE", checkerConfig)

	helperConfig("CHECKER_NAMESPACE", checkerConfig)

	senderAPI := "http://" + checkerConfig["SENDER_SERVICE"] + "." + checkerConfig["CHECKER_NAMESPACE"] + ".svc.cluster.local:" + checkerConfig["SENDER_API_PORT"]

	var clientset *kubernetes.Clientset
	var config *rest.Config
	_, ok = os.LookupEnv("DEVELOP_MODE")
	if ok {
		fmt.Println("DEV: kubernetes stub inserted")
		config = nil
		clientset = nil
	} else {
		// Get more needed variables
		helperConfig("SCREENSHOT_API_PORT", checkerConfig)
		helperConfig("COMPARATOR_API_PORT", checkerConfig)
		helperConfig("SCREENSHOT_SERVICE", checkerConfig)
		helperConfig("COMPARATOR_SERVICE", checkerConfig)

		config, err = rest.InClusterConfig()
		if err != nil {
			panic(err.Error())
		}

		clientset, err = kubernetes.NewForConfig(config)
		if err != nil {
			panic(err.Error())
		}
	}

	router := mux.NewRouter()

	testRouter := mux.NewRouter()
	testRouter.HandleFunc("/user", testResponse).Methods("GET")
	authentication := &auth.Authentication{}
	testRouter.Use(authentication.Middleware)

	mount(router, "/passwordless", auth.NewRouter(appURL, jwtKey, senderAPI, db))
	mount(router, "/auth", testRouter)
	apiRouter := swagger.NewRouter(db, jwtKey, clientset, checkerConfig)
	apiRouter.Use(authentication.Middleware)

	mount(router, "/v1", apiRouter)
	mount(router, "/", swagger.HealthRouter())

	corsHost, ok := os.LookupEnv("ALLOWED_ORIGIN")
	if !ok {
		log.Fatalln("could not find ALLOWED_ORIGIN in environment variables. Add it or CORS will be angry.")
	}
	headersOk := handlers.AllowedHeaders([]string{"X-Requested-With", "Content-Type", "Authorization"})
	corsObj := handlers.AllowedOrigins([]string{corsHost})
	methodsOk := handlers.AllowedMethods([]string{"GET", "HEAD", "POST", "PUT", "DELETE", "OPTIONS"})

	port := 8000
	log.Printf("starting server at %s:%d🚀\n", "0.0.0.0", port)
	log.Fatalf("could not start server: %v\n", http.ListenAndServe(fmt.Sprintf(":%d", port), handlers.CORS(corsObj, headersOk, methodsOk)(router)))
}
