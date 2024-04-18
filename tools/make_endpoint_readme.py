import json

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def extract_example(schema, components):
    if '$ref' in schema:
        ref_path = schema['$ref'].split('/components/schemas/', 1)[-1]
        schema = components['schemas'][ref_path]
    if 'example' in schema:
        return schema['example']
    example = {}
    for prop, details in schema.get('properties', {}).items():
        example[prop] = details.get('example', f'example_{prop}')
    return example

def generate_markdown(data):
    components = data.get('components', {})
    endpoints = ["# API Endpoints\n\n"]

    for path, methods in data.get('paths', {}).items():
        for method, details in methods.items():
            endpoint_str = f"### {details.get('summary', 'API Endpoint')}\n\n"
            endpoint_str += f"- **Method**: {method.upper()}\n"
            endpoint_str += f"- **URL**: `{path}`\n"
            endpoint_str += f"- **Description**: {details.get('description', 'No description provided.')}\n"

            # Extracting Request Body Example
            request_body = details.get('requestBody', {})
            if request_body:
                content = request_body.get('content', {}).get('application/json', {})
                schema = content.get('schema', {})
                example = extract_example(schema, components)
                example_json = json.dumps(example, indent=2).replace('\n', '\n  ')
                endpoint_str += f"- **Request Body**:\n  ```json\n  {example_json}\n  ```\n"

            # Handling Responses
            responses = details.get('responses', {})
            for status_code, response in responses.items():
                response_description = response.get('description', '')
                response_content = response.get('content', {}).get('application/json', {})
                response_example = json.dumps(response_content.get('example', {}), indent=2).replace('\n', '\n  ')
                endpoint_str += f"- **Response {status_code}**: {response_description}\n  ```json\n  {response_example}\n  ```\n\n"

            endpoints.append(endpoint_str)

    return "\n".join(endpoints)

def main():
    openapi_data = load_json('openapi.json')  # Load your OpenAPI spec JSON file
    markdown_content = generate_markdown(openapi_data)

    with open('docs/API_ENDPOINTS.md', 'w', encoding='utf-8') as md_file:
        md_file.write(markdown_content)

if __name__ == "__main__":
    main()
