import pytest
from src.channels import channels_create_v1
from src.error import InputError
from src.other import clear_v1
from src.auth import auth_register_v1

    
def test_channels_create_length_of_name():
    clear_v1()
    test_user = auth_register_v1('shaozhen@gmail.com', 'qwe1212', 'shaozhen', 'yan')
    #check the length of name is more than 20 characters
    with pytest.raises(InputError):
        channels_create_v1(test_user, 'A name clearly more than 20 characters', True)
    
#check the channle is public or not
def test_channels_create_public_or_not():
    clear_v1()
    test_user = auth_register_v1('shaozhen@gmail.com', 'qwe1212', 'shaozhen', 'yan')
    
    public_channel_id = channels_create_v1(test_user, "public_channel", True)
    private_channel_id = channels_create_v1(test_user, "private_channel", False)  
    #still need to be added
    
#check the is_public is boolean or not
def test_channels_create_is_public_bool():
    clear_v1()
    test_user = auth_register_v1('shaozhen@gmail.com', 'qwe1212', 'shaozhen', 'yan')
    
    with pytest.raises(InputError):
        channels_create_v1(test_user, 'good_channel', 'not_a_bool')
    
    
    
    
    






