#!/usr/bin/env python3
"""
Use pymongo to interact with mongod
"""
import pymongo


def main():
    """
    Main function and code entry point, print log statistics
    about nginx logs from mongoDB
    log format:
    ----------
    <X> logs:
    Methods:
        method <Method_type>: <Num_of_accs>
                    ....
                    ....
    <X> status check
    """
    client = pymongo.MongoClient()
    db = client.logs
    nginx_collection = db.nginx
    ips = {}

    X_logs = nginx_collection.count()
    get_logs = nginx_collection.count({"method": "GET"})
    post_logs = nginx_collection.count({"method": "POST"})
    put_logs = nginx_collection.count({"method": "PUT"})
    patch_logs = nginx_collection.count({"method": "PATCH"})
    del_logs = nginx_collection.count({"method": "DELETE"})

    X_status_check = nginx_collection.count(
        {"method": "GET", "path": r"/status"}
    )

    result = "{} logs\nMethods:\n\tmethod GET: {}\n\tmethod POST: {}"
    result += "\n\tmethod PUT: {}\n\tmethod PATCH: {}\n\t"
    result += "method DELETE: {}\n{} status check"
    result += "\nIPs:"
    result = result.format(X_logs, get_logs, post_logs,
                           put_logs, patch_logs, del_logs,
                           X_status_check)
    for doc in nginx_collection.find({}, {"ip": True, "_id": False}):
        ips[doc['ip']] = ips.get(doc['ip'], 0) + 1

    sorted_ips = sorted(ips.items(), reverse=True,
                        key=lambda e: (e[1], e[0]))

    for ip in sorted_ips[:10]:
        # print(ip)
        result += f"\n\t{ip[0]}: {ip[1]}"
    print(result)
    return result


if __name__ == "__main__":
    main()
