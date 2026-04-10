#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json as _json
import requests as _requests
from fasttest.common.dict import Dict


class ApiResponse:
    """接口响应封装，支持链式断言 + 点号访问响应体"""

    def __init__(self, response: _requests.Response):
        self._response = response
        self.status_code = response.status_code
        self._json_data = None
        try:
            raw = response.json()
            self._json_data = Dict(raw) if isinstance(raw, dict) else raw
        except Exception:
            self._json_data = None

    def json(self):
        return self._json_data

    def text(self):
        return self._response.text

    # ── 链式断言 ──────────────────────────────────────────

    def assert_ok(self):
        """断言 HTTP 状态码为 200"""
        assert self.status_code == 200, \
            f"期望状态码 200，实际 {self.status_code}，响应体: {self._response.text[:500]}"
        return self

    def assert_status(self, expected: int):
        """断言指定状态码"""
        assert self.status_code == expected, \
            f"期望状态码 {expected}，实际 {self.status_code}"
        return self

    def assert_status_in(self, *expected_codes: int):
        """断言状态码在给定列表中"""
        assert self.status_code in expected_codes, \
            f"期望状态码在 {expected_codes} 中，实际 {self.status_code}"
        return self

    def assert_field(self, *fields: str):
        """断言响应体中包含指定字段（支持多个）"""
        data = self._json_data
        assert data is not None, "响应体无法解析为 JSON"
        for field in fields:
            assert field in data, \
                f"响应体中缺少字段 '{field}'，实际字段: {list(data.keys()) if hasattr(data, 'keys') else data}"
        return self

    def assert_field_value(self, field: str, expected):
        """断言响应体某字段的值"""
        data = self._json_data
        assert data is not None, "响应体无法解析为 JSON"
        actual = data[field] if field in data else None
        assert actual == expected, \
            f"字段 '{field}' 期望 {expected}，实际 {actual}"
        return self


class Requests:
    """接口测试请求封装，支持 Bearer Token、自定义请求头、base_url"""

    def __init__(self):
        self._base_url: str = ''
        self._headers: dict = {}
        self._token: str = ''
        self._session = _requests.Session()
        self.call_log: list = []  # 记录每次请求/响应，供报告展示

    # ── 配置方法 ──────────────────────────────────────────

    def set_base_url(self, base_url: str):
        """设置 base_url，用例中只需传相对路径"""
        self._base_url = base_url.rstrip('/')

    def set_bearer_token(self, token: str):
        """设置 Bearer Token"""
        self._token = token

    def clear_token(self):
        """清除 Token（用于测试未授权场景）"""
        self._token = ''

    def set_headers(self, headers: dict):
        """设置全局请求头（追加/覆盖）"""
        self._headers.update(headers)

    def clear_headers(self):
        """清除所有自定义请求头"""
        self._headers = {}

    def clear_call_log(self):
        """清除请求记录（每条用例结束后调用）"""
        self.call_log = []

    # ── 内部辅助 ──────────────────────────────────────────

    def _build_url(self, url: str) -> str:
        if url.startswith('http://') or url.startswith('https://'):
            return url
        return self._base_url + '/' + url.lstrip('/')

    def _build_headers(self, extra_headers: dict = None) -> dict:
        headers = {}
        headers.update(self._headers)
        if self._token:
            headers['Authorization'] = f'Bearer {self._token}'
        if extra_headers:
            headers.update(extra_headers)
        return headers

    def _record(self, method: str, full_url: str, params, json_body, data,
                response: _requests.Response) -> None:
        """记录一次请求/响应到 call_log"""
        entry = {'method': method, 'url': full_url}
        if params:
            entry['params'] = _json.dumps(params, ensure_ascii=False, indent=2)
        if json_body is not None:
            entry['body'] = _json.dumps(json_body, ensure_ascii=False, indent=2)
        elif data is not None:
            entry['body'] = str(data)
        entry['status_code'] = response.status_code
        try:
            resp_json = response.json()
            entry['response'] = _json.dumps(resp_json, ensure_ascii=False, indent=2)[:3000]
        except Exception:
            entry['response'] = response.text[:500]
        self.call_log.append(entry)

    # ── HTTP 方法 ──────────────────────────────────────────

    def get(self, url: str, params: dict = None, headers: dict = None) -> ApiResponse:
        full_url = self._build_url(url)
        merged_headers = self._build_headers(headers)
        response = self._session.get(full_url, params=params, headers=merged_headers)
        self._record('GET', full_url, params, None, None, response)
        return ApiResponse(response)

    def post(self, url: str, json: dict = None, data=None,
             params: dict = None, headers: dict = None) -> ApiResponse:
        full_url = self._build_url(url)
        merged_headers = self._build_headers(headers)
        response = self._session.post(
            full_url, json=json, data=data,
            params=params, headers=merged_headers
        )
        self._record('POST', full_url, params, json, data, response)
        return ApiResponse(response)

    def put(self, url: str, json: dict = None, data=None,
            params: dict = None, headers: dict = None) -> ApiResponse:
        full_url = self._build_url(url)
        merged_headers = self._build_headers(headers)
        response = self._session.put(
            full_url, json=json, data=data,
            params=params, headers=merged_headers
        )
        self._record('PUT', full_url, params, json, data, response)
        return ApiResponse(response)

    def delete(self, url: str, params: dict = None, headers: dict = None) -> ApiResponse:
        full_url = self._build_url(url)
        merged_headers = self._build_headers(headers)
        response = self._session.delete(full_url, params=params, headers=merged_headers)
        self._record('DELETE', full_url, params, None, None, response)
        return ApiResponse(response)
