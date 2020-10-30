const LocalStorageService = (function () {
    let _service;

    function _getService() {
        if (!_service) {
            _service = this;
        }
        return _service
    }

    function _setToken(tokenObj) {
        localStorage.setItem('access_token', tokenObj.access);
        localStorage.setItem('refresh_token', tokenObj.refresh);
    }

    function _getAccessToken() {
        return localStorage.getItem('access_token');
    }

    function _getRefreshToken() {
        return localStorage.getItem('refresh_token');
    }

    function _clearToken() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    }

    return {
        getService: _getService,
        setToken: _setToken,
        getAccessToken: _getAccessToken,
        getRefreshToken: _getRefreshToken,
        clearToken: _clearToken
    }
})();

export default LocalStorageService;
