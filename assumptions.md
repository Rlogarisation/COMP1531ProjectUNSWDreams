# Assumption

## Iteration 1

## Assumptions for auth.py:
* We assume that auth_user_id is the same with u_id,  
  which are both used to identify a unique user.
* auth_user_id and u_id are integers, like 0, 1, 2, 3, 4......  
  For example, the auth_user_id of the first registered user is 0, the auth_user_id of the second user is 1.
* One user can log in by different sessions at the same time.  
The user log out one session will not affect other sessions.
  
## Assumptions for channel.py:
* A registered user needs to log in or register, before he/she does any operations with channel.
* If a user has already been invited to a channel, there is no effect if the user is invited to the channel again.
* A global owner has all owner permissions in the channel he/she joined in.  
  However, the global owner is still a member of the channel if the owner does not add the global owner to be an owner of  
  the channel.
* if the only owner leaves the channel, and there is still member in the channel,  
  the first member will automatically become the owner of the channel.  
  
## Assumptions for channels.py:
* channel_id are non-negative integers, like 0, 1, 2, 3, 4......  
  channel_id is a unique id, which is to identify a channel.
* We assume that is_public for the channel is type of bool. True means public and False means private.  

## Assumptions for message.py:
* The format of the shared message is  
  optional message  
  """  
  original message  
  """
* If the original message is edited, the content of the shared message will not automatically be edited.  
* If the message is edited, the time created will not change
 
## Assumptions for dm.py:
* If the only owner leaves the dm, and there is still member in the dm  
the first member will automatically become the owner of the dm.  
* If there are two people in the dm and one person left, the dm still exists.  
If the only member left, the dm still exists.
  
## Assumptions for user.py:  
* If a user is removed from the Dreams, his/hers name_first will be replaced by 'Removed',  
and his/hers name_last will be replaced by 'user'.

## Assumptions for other.py:
* In search/v2, The message that match the query is case-insensitive.
* The order of the notifications is from the most to least recent.  
* If more than one user are tagged in one message, all the tagged users will receive the notification.
* Sending message, editinging message and sharing message can tag users.