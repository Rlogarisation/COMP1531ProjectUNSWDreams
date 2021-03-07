# Assumption

## Iteration 1

## Assumptions for auth.py:
* In iteration 1, we assume that auth_user_id is the same with u_id,  
which are both used to identify a unique user.
* auth_user_id and u_id are integers, like 0, 1, 2, 3, 4......
  For example, the auth_user_id of the first registered user is 0, the auth_user_id of the second user is 1.
* We assume that a user can only log in once before log out, which means the user will not log in again if the user has 
already logged in.
  
## Assumptions for channel.py:
* A registered user needs to log in before he/she does any operations with channel.
* If a user has already been invited to a channel, there is no effect if the user is invited to the channel again.
* A global owner has all owner permissions in the channel he/she joined in.  
  However, the global owner is still a member of the channel if the owner does not add the global owner to be an owner of  
  the channel.  

## Assumptions for channels.py:
* channel_id are non-nenagtive integers, like 0, 1, 2, 3, 4......  
  channel_id is a unique id, which is to identify a channel.
  