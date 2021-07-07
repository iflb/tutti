function importConfig(name) {
    return require(`./platform-configs/${name}.js`).default;
}

const rfr = document.referrer;

const conds = [
    ['tutti-market', (
        rfr.length>0 &&
        rfr.startsWith("http://localhost:8888")
    )],

    ['mturk', (
        rfr.length>0 &&
        [
            'https://worker.mturk.com',
            'https://workersandbox.mturk.com'
        ].some( (url) => (rfr.startsWith(url)) )
    )],

    ['private', true]
]

export const platformConfig = importConfig( conds.find((c) => (c[1]))[0] );
