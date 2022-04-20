if [ -e .env ]; then
        mv .env tmp
fi
pytest -k "not test_api_endpoint_"

if [ -e tmp ]; then
        mv tmp .env
fi
pytest -k "test_api_endpoint_"
