const ghpages = require('gh-pages');

const now = new Date()
const isoString = now.toISOString()

ghpages.publish(
    'dist',
    {
        message: `Github Pages Built on ${isoString}`
    },
    err => {
        console.log(err)
    }
)
