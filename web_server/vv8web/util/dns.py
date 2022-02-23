import dns.message

dns_servers = [
    '1.1.1.1', # cloudflare
    '1.0.0.1', # cloudflare
    '8.8.8.8', # google
    '8.8.4.4'  # google
]

use_tls = True

async def dns_tls_lookup(domain_name):
    query = snd.message.make_query(domain_name, 'A')
    resp = await dns.asyncquery.tls(query, dns_servers[0])
    breakpoint()
    print(resp)

async def dns_lookup(domain_name):
    query = snd.message.make_query(domain_name, 'A')
    resp = await dns.asyncquery.udp(query, dns_servers[0])
    return resp

async def dns_lookup(domain_name):
    if use_tls:
        dns_tls_lookup(domain_name)

if __name__ == '__main__':
    import asyncio
    asyncio.run(dns_lookup('google.com'))
