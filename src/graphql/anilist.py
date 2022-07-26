import requests
from addict import Dict
from graphql.queries import queries

def fetchUser(username):
  munchData = Dict(requests.post('https://graphql.anilist.co/', json={ 'query': queries.user, 'variables': {'name':username} }).json())
  return munchData.data.User

def fetchUserStats(userId):
  munchData = Dict(requests.post('https://graphql.anilist.co/', json={ 'query': queries.userStats, 'variables': {'userId':userId} }).json())
  return munchData.data.User

def search(query):
  munchData = Dict(requests.post('https://graphql.anilist.co/', json={ 'query': queries.search, 'variables': {'search':query} }).json())
  return munchData.data.Page.media

def fetch(id):
  munchData = Dict(requests.post('https://graphql.anilist.co/', json={ 'query': queries.media, 'variables': {'id':id} }).json())
  return munchData.data.Media

def fetchUsersEntry(userIds, mediaId):
  munchData = Dict(requests.post('https://graphql.anilist.co/', json={ 'query': queries.entry, 'variables': {'userIds': userIds, 'mediaId': mediaId} }).json())
  return munchData.data.Page.mediaList

def fetchUserFavourites(userId):
  munchData = Dict(requests.post('https://graphql.anilist.co/', json={ 'query': queries.favourites, 'variables': {'userId': userId} }).json())
  return munchData.data.User.favourites

def fetchActivity(userId):
  munchData = Dict(requests.post('https://graphql.anilist.co/', json={ 'query': queries.activity, 'variables': {'userId': userId} }).json())
  return munchData.data.Activity

def searchStaff(query):
  munchData = Dict(requests.post('https://graphql.anilist.co/', json={ 'query': queries.searchStaff, 'variables': {'query': query} }).json())
  return munchData.data.Page.staff

def fetchStaff(id):
  munchData = Dict(requests.post('https://graphql.anilist.co/', json={ 'query': queries.staff, 'variables': {'id': id} }).json())
  return munchData.data.Staff