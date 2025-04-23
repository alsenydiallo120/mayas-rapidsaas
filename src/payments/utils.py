def site_domain_to_stripe_redirect_format(site_domain: str, port: int, is_https: bool = True) -> str:
    if site_domain == 'localhost' or site_domain == '127.0.0.1':
        # noinspection HttpUrlsUsage
        return f"http://{site_domain}:{port}"

    if is_https:
        return f"https://{site_domain}"
    # noinspection HttpUrlsUsage
    return f"http://{site_domain}"
