from src.data_file import Permission, data
from src.auth import get_user_by_uid, session_to_token, token_to_session, get_user_by_token, \
    is_email_valid
from src.error import InputError, AccessError
from PIL import Image
import requests
import os
from src import config
import urllib.request
import io


def user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end, y_end):
    user = get_user_by_token(token)
    if user is None:
        raise AccessError(description="Token passed in is invalid")

    # get the image from url
    response = requests.get(img_url, stream=True)
    if response.status_code != 200:
        raise InputError(description="img_url returns an HTTP status other than 200.")

    # check the format of the image
    # image = Image.open(response.raw)
    image = Image.open(io.BytesIO(response.content))
    if image.format != 'JPEG':
        raise InputError(description="Image uploaded is not a JPG")

    # check whether the input bounds are valid
    width, height = image.size
    if x_start > width or x_end > width or x_start < 0 or x_end < 0 or x_start >= x_end:
        raise InputError(description="x_start or x_end are not within the dimensions of the image")
    if y_start > height or y_end > height or y_start < 0 or y_end < 0 or y_start >= y_end:
        raise InputError(description="y_start or y_end are not within the dimensions of the image")

    # save the original image locally
    path = 'src/static/'
    # path = './src/static'
    if not os.path.exists(path):
        os.mkdir(path)
    path = path + str(user.u_id) + '.jpg'
    user.image_path = path
    # urllib.request.urlretrieve(img_url, path)

    # crop the image
    image_cropped = image.crop((x_start, y_start, x_end, y_end))
    # overwrite the original image by the cropped image
    image_cropped.save(path)

    # generate the image_url
    user.image_url = config.url + path

    return {}


img_url = "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fbenyouhuifile.it168.com%2Fforum%2Fday_100124%2F20100124_9709b2f5aa84728f755cmxD7h4CyWGcu.jpeg&refer=http%3A%2F%2Fbenyouhuifile.it168.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1621152937&t=2e1e7dee322cadb76f263e7b5fd0f681"
response = requests.get(img_url, stream=True)
if response.status_code == 200:
    open('img.jpeg', 'wb').write(response.content)  # 将内容写入图片
    print("done")
image = Image.open('img.jpeg')
image.show()
