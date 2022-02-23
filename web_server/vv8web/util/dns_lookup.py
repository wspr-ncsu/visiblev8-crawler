import dns
import dns.message
import dns.asyncquery
import dns.asyncresolver


dns_servers = [
    '1.1.1.1', # cloudflare
    '1.0.0.1', # cloudflare
    '8.8.8.8', # google
    '8.8.4.4'  # google
]

use_tls = True


async def dns_exists(domain_name):
    qname = dns.name.from_text(domain_name)
    query = dns.message.make_query(qname, 'A')
    for dns_server in dns_servers:
        try:
            if use_tls:
                resp = await dns.asyncquery.tls(query, dns_server)
            else:
                resp = await dns.asyncquery.udp(query, dns_server)
            if resp.rcode() == dns.rcode.NOERROR:
                return True
            elif resp.rcode() == dns.rcode.NXDOMAIN:
                return False
        except ex:
            # Failed to connect to dns server, try next
            continue
    return False
