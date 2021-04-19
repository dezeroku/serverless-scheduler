package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"strings"

	"github.com/d0ku/monitor_page/manager/v2/auth"
	"github.com/d0ku/monitor_page/manager/v2/common"
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

		databaseType := common.Env("DATABASE_TYPE", "postgres")
		db, err = gorm.Open(databaseType, databaseConnString)
	}

	if err != nil {
		panic("failed to connect database")
	}

	defer db.Close()

	jwtKey, ok := os.LookupEnv("JWT_KEY")
	if !ok {
		log.Fatalln("could not find JWT_KEY on environment variables")
	}

	appURL, ok := os.LookupEnv("APP_URL")
	if !ok {
		log.Fatalln("could not find APP_URL on environment variables")
	}

	senderAPI, ok := os.LookupEnv("SENDER_API")
	if !ok {
		log.Fatalln("could not find SENDER_API on environment variables")
	}

	checkerImage, ok := os.LookupEnv("CHECKER_IMAGE")
	if !ok {
		log.Fatalln("could not find CHECKER_IMAGE on environment variables")
	}

	var clientset *kubernetes.Clientset
	var config *rest.Config
	_, ok = os.LookupEnv("DEVELOP_MODE")
	if ok {
		fmt.Println("DEV: kubernetes stub inserted")
		config = nil
		clientset = nil
	} else {
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
	apiRouter := swagger.NewRouter(db, jwtKey, clientset, checkerImage)
	apiRouter.Use(authentication.Middleware)

	mount(router, "/", apiRouter)

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
