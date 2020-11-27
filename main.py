from pymongo import MongoClient  # pymongo를 임포트 하기
import requests
import xml.etree.ElementTree as ET


client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbMediRecord  # 'dbMediRecord'라는 이름의 db를 만들거나 사용합니다.

global infos # 약정보 리스트를 저장할 list 초기화한다
global info # 각 약정보를 저장할 dict 초기화한다
global wrong_status
infos = []  # 약정보 리스트를 저장할 list 초기화한다
wrong_status = []


def db_store(store_list):
    global infos # 약정보 리스트를 저장할 list 초기화한다
    global wrong_status

    for i in store_list:  # 233
        url = "http://apis.data.go.kr/1470000/MdcinGrnIdntfcInfoService/getMdcinGrnIdntfcInfoList?ServiceKey=3ZPAM2feMz32pRzpOJK5r24532tEUzWc2dOk2iU6Xb9Vdf03hLpU1Q07TvHodKfMw9aulvcNQHLrZR6JylDzfg%3D%3D&numOfRows=100&pageNo=" + str(
            i)
        response = requests.get(url)
        status = response.status_code
        text = response.text
        print(status)
        print(text)
        root = ET.fromstring(response.text)

        if status == 200:
            if i in wrong_status:
                wrong_status.remove(i)
            iter_element = root.iter(tag="item")  # item 태그 iterator를 가져옵니다
            for element in iter_element:  # item 태그를 순회합니다
                info = {}  # 각 약정보를 저장할 dict 초기화한다
                info['item_name'] = element.find("ITEM_NAME").text  # ITEM_NAME 태그 값을 저장합니다
                info['item_image'] = element.find("ITEM_IMAGE").text  # ITEM_IMAGE 태그 값을 저장합니다
                infos.append(info)  # 리스트에 정보를 저장합니다
        else:
            wrong_status.append(i)
            continue
    if len(wrong_status) != 0:
        db_store(wrong_status)


def post_infos(store_list):
    print("시작")

    db_store(store_list)

    print(infos)  # 결과를 출력한다
    print(len(infos))
    db.infos.insert_many(infos)

    print("끝")


num_of_d = []
for i in range(1, 233): # 233
    num_of_d.append(i)
post_infos(num_of_d)
