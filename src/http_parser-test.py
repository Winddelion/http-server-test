#THIS IS USED TO TEST THE LOGIC OF HTTP PARSER. It doesn't goes into actual project

http_req = b"""GET /path?query=value HTTP/1.1\r\nHost: example.com\r\nUser-Agent: Mozilla/5.0\r\nContent-Type: application/json\r\nContent-Length: 18\r\n\r\n{"key": "value"}"""

def http_parse(request):
    http_lines = request.decode("utf-8").split("\r\n")

    empty_index = http_lines.index('') if '' in http_lines else -1

    if empty_index != -1:
        header = http_lines[:empty_index]
        body = http_lines[empty_index + 1]
        return header, body
    else:
        return http_lines, None

def line_parse(head: list):
    if not head:
        raise ValueError("Empty header list")
    request_line = head[0]
    request_parts = request_line.split(' ')
    if len(request_parts) >= 2:
        method = request_parts[0]
        path = request_parts[1]
        return (method, path)

header, body = http_parse(http_req)
print(f"Header: {header}")
print(f"Body: {body}")

print("\n Parsing lines:\n")

method, path = line_parse(header)
print(f"METHOD: {method}")
print(f"PATH: {path}")
