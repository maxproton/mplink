import argparse

from tqdm import tqdm

import banner
import module_web

def image_type(lnk):
    if lnk.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp')):
        return True
    else:
        return False

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process a file and perform operations on its lines.")
    parser.add_argument("-d", "--domain", type=str, required=True, help="Domain entry point")
    parser.add_argument("-v", "--verbose", action="store_true", help="Shows you everything!")
    parser.add_argument("-c", "--csv", action="store_true", required=False,
                        help="Generates a report in csv format")
    return parser.parse_args()

if __name__ == '__main__':
    deadlink = {}
    main = {}
    unreachable_status_codes = [400, 403, 404, 408, 410, 421, 429, 500, 502, 503, 504, 511]

    print(banner.banner)
    args = parse_arguments()
    if "https://" not in args.domain:
        domain = "https://" + args.domain
    else:
        domain = args.domain

    links_sitemap = module_web.get_sitemap_and_robot_links(domain, args.verbose)
    main_page_links = module_web.extract_links(domain, args.verbose)
    all_links = list(set(links_sitemap + main_page_links))

    # Check what we have none of them are dead
    if args.verbose:
        print(f"[Info] Checking how many links are dead before we go any further")
    with tqdm(total=len(all_links), desc="Processing content", unit="links") as pbar:
        for link in all_links:
            return_status = module_web.check_link(link)
            if return_status in unreachable_status_codes:
                deadlink[link] = link
                all_links.remove(link)
                if args.verbose:
                    print(f"[Info] Found a dead link {link}")
            else:
                main[link] = link
            pbar.update(1)

    if args.verbose:
        print(f"[Info] Now checking to see how many of the links are garbage")
    for base_links in all_links:
        if not image_type(base_links) and module_web.is_same_domain(base_links, domain):
            additional_links = module_web.extract_links(base_links)
            for addit in additional_links:
                main[addit] = base_links

    # we should not have a ist of extensive domain links and also some external links now lets check to see if any are dead
    qty = len(all_links)

    with tqdm(total=len(main), desc="Processing content", unit="link") as pbar:
        for link, base in main.items():
            return_status = module_web.check_link(link)
            if return_status in unreachable_status_codes:
                deadlink[link] = base
            pbar.update(1)

    if args.verbose:
        for link, base in main.items():
            print(f"[link] {link} located on base url: {base}")
    print(f"[Info] {qty} links discovered from sitemap and inital page")
    print(f"[Info] Following deadlinks detected")
    for dead, base in deadlink.items():
        print(f"[dead][{base}]{dead}")

    print(module_web.generate_csv_summary(main, domain, "all-links-report"))
    print(module_web.generate_csv_summary(deadlink, domain, "deadlink-report"))
