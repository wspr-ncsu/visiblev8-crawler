export function logBreakerModule() {
    const fs = require('fs')
    try {
        const data = fs.readFileSync('web_server/logs/akamai.net.txt', 'utf8')
        console.log(data)
        return data
    } catch (err) {
        console.error(err)
    }
    
}