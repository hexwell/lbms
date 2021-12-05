importScripts('/static/js/sw-toolbox.js');

toolbox.router.default = toolbox.networkFirst;
toolbox.options.networkTimeoutSeconds = 5;

toolbox.router.get('icons/*', toolbox.fastest);
