import requests

base_orders_url = "https://www.swiggy.com/dapi/order/all?order_id="
changing_orders_url = base_orders_url
mobile_headers = {
    "platform": "mweb",
    "Cookie": "__SW=64ZWgaDZD8vGOgl7GuqDS9JhRxHXYWmr; _device_id=39ec0a26-c04a-a219-ea07-391b31d23322; userLocation={%22lat%22:%2221.99740%22%2C%22lng%22:%2279.00110%22%2C%22address%22:%22%22%2C%22area%22:%22%22%2C%22showUserDefaultAddressHint%22:false}; fontsLoaded=1; _gcl_au=1.1.2017180.1756151167; _gid=GA1.2.1539384182.1756151167; _is_logged_in=1; _session_tid=6afee8d17db8456fe6147837622a16255d0fad58c9a2456da4b69e4813543a8788b6f0e478469531e0b50289c565f578539decd6be6be27052ba902e1a2efd1d287e9332b2ee3db1477c503a432033a87251bf6af3df5a8cdc704258fe243b9b007ff58399315e2956b05617768089b8; application_name=; category=; x-channel=; _swuid=39ec0a26-c04a-a219-ea07-391b31d23322; _sid=mi4d52a3-f7d1-4459-a485-daeab1d7df81; _ga_YE38MFJRBZ=GS2.1.s1756161113$o3$g1$t1756162019$j60$l0$h0; _ga_34JYJ0BCRN=GS2.1.s1756161113$o3$g1$t1756162019$j60$l0$h0; _ga_X3K3CELKLV=GS2.1.s1756162021$o1$g0$t1756162021$j60$l0$h0; AMP_TOKEN=%24NOT_FOUND; _ga=GA1.2.469705141.1756151167; _gat_UA-53591212-9=1"
}
headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "Referer": "https://www.swiggy.com/my-account",
    "platform": "dweb",
    "Cookie": "__SW=64ZWgaDZD8vGOgl7GuqDS9JhRxHXYWmr; _device_id=39ec0a26-c04a-a219-ea07-391b31d23322; _sid=mi15dfbd-111b-4ba2-89e7-31ea1a86c92f; userLocation={%22lat%22:%2221.99740%22%2C%22lng%22:%2279.00110%22%2C%22address%22:%22%22%2C%22area%22:%22%22%2C%22showUserDefaultAddressHint%22:false}; fontsLoaded=1; _gcl_au=1.1.2017180.1756151167; _gid=GA1.2.1539384182.1756151167; _is_logged_in=1; _session_tid=6afee8d17db8456fe6147837622a16255d0fad58c9a2456da4b69e4813543a8788b6f0e478469531e0b50289c565f578539decd6be6be27052ba902e1a2efd1d287e9332b2ee3db1477c503a432033a87251bf6af3df5a8cdc704258fe243b9b007ff58399315e2956b05617768089b8; _gat_0=1; _ga=GA1.1.469705141.1756151167; _ga_YE38MFJRBZ=GS2.1.s1756151167$o1$g1$t1756152321$j59$l0$h0; _ga_34JYJ0BCRN=GS2.1.s1756151166$o1$g1$t1756152321$j59$l0$h0"
}

city_filters = ["Pune", "Hyderabad", "Thane"]
target_city = "Pune"
totalSum = 0.0
last_order_time_recorded, last_recorded_order_id = "", 0

for j in range(1000):
    response = requests.get(changing_orders_url, headers=headers)
    orders = response.json()['data']['orders']      # List of dicts
    len_of_orders = len(orders)
    for i, order in enumerate(orders):
        if order['delivery_address']['city'] == target_city:
            totalSum += round(float(order['order_total']), 2)
        last_order_id = str(order['order_id'])
        last_recorded_order_id = last_order_id
        changing_orders_url = base_orders_url + last_order_id
        last_order_time_recorded = order["updated_at"]

    print(f"At page: {j+1}, the Updated Spending Amount has reached to: {totalSum} ordering from: {order['restaurant_name']} with Order PK: {last_recorded_order_id} on {order['updated_at']}")

print(f"Total Order Amount: {totalSum} reached till {last_order_time_recorded} with Order PK: {last_recorded_order_id}")
