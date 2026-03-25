import json

class Request(object):

    def __init__(self) -> None:
        self.request_list = []

    def handle_request(self, request):
        pass

    def handle_response(self, response):

        try:
            data = {
                'url': response.url,
                'request': {
                    'method': response.request.method,
                    'headers': response.request.headers,
                    'data': response.request.post_data_json
                },
                'response': {
                    'ok': response.ok,
                    'status': response.status,
                    'data': response.json()
                }
            }
            self.request_list.append(data)
        except Exception as e:
            pass