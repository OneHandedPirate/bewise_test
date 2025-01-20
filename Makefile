create_env:
	touch .env
	echo "DB__USER='postgres'\nDB__PASSWORD='postgres'\nDB__NAME='bewise'\nDB__PORT=5432\nDB__HOST='db'\n\nGUNICORN__PORT=8000\n\nFASTAPI__TITLE='Bewise test'\nFASTAPI__DESCRIPTION='Bewise test'\n\nKAFKA__HOST='kafka'\nKAFKA__PORT=9092\nKAFKA__TOPIC_NAME='test-topic'\nKAFKA__ZOOKEEPER_PORT=2181" > .env
