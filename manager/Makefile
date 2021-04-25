info:
	echo "Use make testing_mode to run dev with dummy data"

dev:
	CHECKER_NAMESPACE=testing CHECKER_IMAGE=test_checker_image ALLOWED_ORIGIN="*" APP_URL=test_url SENDER_SERVICE=test_sender_service SENDER_API_PORT=test_sender_port JWT_KEY=testing DEVELOP_MODE=1 go run main.go
