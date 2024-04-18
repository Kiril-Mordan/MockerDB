# create API_ENDPOINTS
python ./tools/make_endpoint_readme.py

# create README
cp docs/README_base.md  README.md
cat docs/API_ENDPOINTS.md >> README.md