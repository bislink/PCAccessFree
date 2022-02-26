//<-- Service Worker - Win 2016 - tap.a2z.blue/pcaccessfree/service-worker.js //-->

'use strict';

const CACHE_NAME = 'pcaf-static-cache-v11';
const DATA_CACHE_NAME = 'pcaf-data-cache-v11';

const FILES_TO_CACHE = [
    'index.htm',
    'index.cgi',
    'index.css',
    'index.js',
    'offline.htm'
];

self.addEventListener('install', (evt) => {
    console.log('PCAccessFree   Install');
    // CODELAB: Precache static resources here.
    evt.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('PCAccessFree   Pre-caching offline page');
            return cache.addAll(FILES_TO_CACHE);
        })
    );

    self.skipWaiting();
});

self.addEventListener('activate', (evt) => {
    console.log('PCAccessFree   Activate');
    // CODELAB: Remove previous cached data from disk.
    evt.waitUntil(
        caches.keys().then((keyList) => {
            return Promise.all(keyList.map((key) => {
                if (key !== CACHE_NAME && key !== DATA_CACHE_NAME) {
                    console.log('PCAccessFree   Removing old cache', key);
                    return caches.delete(key);
                }
            }));
        })
    );

    self.clients.claim();
});

self.addEventListener('fetch', (evt) => {
    console.log('PCAccessFree   Fetch', evt.request.url);
    // CODELAB: Add fetch event handler here.
    if (evt.request.url.includes('/github/pcaccessfree/')) {
        console.log('PCAccessFree Fetch (data)', evt.request.url);
        evt.respondWith(
            caches.open(DATA_CACHE_NAME).then((cache) => {
                return fetch(evt.request)
                    .then((response) => {
                        // If the response was good, clone it and store it in the cache.
                        if (response.status === 200) {
                            cache.put(evt.request.url, response.clone());
                        }
                        return response;
                    }).catch((err) => {
                        // Network request failed, try to get it from the cache.
                        return cache.match(evt.request);
                    });
            }));
        return;
    }
    evt.respondWith(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.match(evt.request)
                .then((response) => {
                    return response || fetch(evt.request);
                });
        })
    );

});
