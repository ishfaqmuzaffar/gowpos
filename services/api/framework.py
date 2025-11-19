"""A tiny HTTP framework for tests and demos."""
from __future__ import annotations

import re
from http import HTTPStatus
from types import SimpleNamespace
from typing import Any, Callable, Dict, Iterable, List, Optional


class HTTPException(Exception):
    """Exception raised for HTTP errors."""

    def __init__(self, status_code: int, detail: str):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


class status:
    HTTP_200_OK = HTTPStatus.OK
    HTTP_201_CREATED = HTTPStatus.CREATED
    HTTP_204_NO_CONTENT = HTTPStatus.NO_CONTENT
    HTTP_400_BAD_REQUEST = HTTPStatus.BAD_REQUEST
    HTTP_401_UNAUTHORIZED = HTTPStatus.UNAUTHORIZED
    HTTP_404_NOT_FOUND = HTTPStatus.NOT_FOUND


class Request:
    def __init__(self, app: "Application", method: str, path: str, headers: Optional[Dict[str, str]] = None, body: Optional[dict] = None):
        self.app = app
        self.method = method.upper()
        self.path = path
        self.headers = {k.lower(): v for k, v in (headers or {}).items()}
        self._json = body or {}
        self.path_params: Dict[str, str] = {}

    def json(self) -> dict:
        return self._json


class Response:
    def __init__(self, body: Any = None, status_code: int = status.HTTP_200_OK):
        self.body = body
        self.status_code = int(status_code)

    def json(self) -> Any:
        return self.body


class Route:
    def __init__(self, method: str, path: str, handler: Callable):
        self.method = method.upper()
        self.path = self._normalize_path(path)
        self.handler = handler
        self.param_names = re.findall(r"{([^}]+)}", self.path)
        regex_path = re.sub(r"{([^}]+)}", r"(?P<\1>[^/]+)", self.path)
        self.pattern = re.compile(f"^{regex_path}$")

    @staticmethod
    def _normalize_path(path: str) -> str:
        if not path.startswith("/"):
            path = f"/{path}"
        if len(path) > 1 and path.endswith("/"):
            path = path[:-1]
        return path

    def matches(self, method: str, path: str) -> Optional[Dict[str, str]]:
        if method.upper() != self.method:
            return None
        match = self.pattern.match(path.rstrip("/") or "/")
        if not match:
            return None
        return match.groupdict()


class Router:
    def __init__(self, prefix: str = "", tags: Optional[Iterable[str]] = None):
        self.prefix = prefix.rstrip("/") if prefix not in ("", "/") else prefix
        self.routes: List[Route] = []
        self.tags = list(tags or [])

    def _full_path(self, path: str) -> str:
        path = path or ""
        if path == "/":
            path = ""
        base = self.prefix
        if not base:
            return path or "/"
        if not path:
            return base or "/"
        return f"{base}/{path.lstrip('/')}"

    def _add_route(self, method: str, path: str, handler: Callable) -> Callable:
        full_path = self._full_path(path)
        self.routes.append(Route(method, full_path, handler))
        return handler

    def get(self, path: str):
        def decorator(func: Callable) -> Callable:
            return self._add_route("GET", path, func)

        return decorator

    def post(self, path: str):
        def decorator(func: Callable) -> Callable:
            return self._add_route("POST", path, func)

        return decorator

    def put(self, path: str):
        def decorator(func: Callable) -> Callable:
            return self._add_route("PUT", path, func)

        return decorator

    def delete(self, path: str):
        def decorator(func: Callable) -> Callable:
            return self._add_route("DELETE", path, func)

        return decorator


class Application:
    def __init__(self, title: str):
        self.title = title
        self.routes: List[Route] = []
        self.middleware: List[Callable[[Request, Callable[[Request], Response]], Response]] = []
        self.state = SimpleNamespace()

    def include_router(self, router: Router) -> None:
        self.routes.extend(router.routes)

    def add_middleware(self, middleware_cls, **kwargs) -> None:
        self.middleware.append(middleware_cls(**kwargs))

    def handle_request(self, method: str, path: str, headers: Optional[Dict[str, str]] = None, body: Optional[dict] = None) -> Response:
        request = Request(self, method, Route._normalize_path(path), headers, body)
        for route in self.routes:
            params = route.matches(method, request.path)
            if params is None:
                continue
            request.path_params = params

            def endpoint(req: Request, route=route, params=params):
                return self._call_handler(route.handler, req, params)

            handler = endpoint
            for middleware in reversed(self.middleware):
                next_handler = handler

                def wrap(req: Request, mw=middleware, nxt=next_handler):
                    return mw(req, nxt)

                handler = wrap
            try:
                return handler(request)
            except HTTPException as exc:
                return Response({"detail": exc.detail}, exc.status_code)
        return Response({"detail": "Not Found"}, status.HTTP_404_NOT_FOUND)

    def _call_handler(self, handler: Callable, request: Request, params: Dict[str, str]) -> Response:
        result = handler(request, **params)
        return self._normalize_response(result)

    @staticmethod
    def _normalize_response(result: Any) -> Response:
        if isinstance(result, Response):
            return result
        if isinstance(result, tuple):
            body, status_code = result
            return Response(body, status_code)
        return Response(result)


class TestResponse:
    def __init__(self, response: Response):
        self._response = response
        self.status_code = response.status_code

    def json(self) -> Any:
        return self._response.json()


class TestClient:
    def __init__(self, app: Application):
        self.app = app

    def request(self, method: str, path: str, json: Optional[dict] = None, headers: Optional[Dict[str, str]] = None) -> TestResponse:
        response = self.app.handle_request(method, path, headers=headers, body=json)
        return TestResponse(response)

    def get(self, path: str, headers: Optional[Dict[str, str]] = None):
        return self.request("GET", path, headers=headers)

    def post(self, path: str, json: Optional[dict] = None, headers: Optional[Dict[str, str]] = None):
        return self.request("POST", path, json=json, headers=headers)

    def put(self, path: str, json: Optional[dict] = None, headers: Optional[Dict[str, str]] = None):
        return self.request("PUT", path, json=json, headers=headers)

    def delete(self, path: str, headers: Optional[Dict[str, str]] = None):
        return self.request("DELETE", path, headers=headers)
