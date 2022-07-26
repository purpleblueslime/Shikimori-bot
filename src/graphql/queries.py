class queries:

  user = '''query($name: String) {
    User (name: $name) {
      id
      name
    }
  }'''

  userStats = '''query($userId: Int) {
    User (id: $userId) {
      createdAt
      stats: statistics {
        anime {
          minutesWatched
        }
      }
    }
  }'''

  search = '''query($search: String) {
    Page (page: 1, perPage: 10) {
      media (search: $search) {
        id
        title {
          english
          romaji
        }
        format
        type
        coverImage {
          color
          extraLarge
        }
        bannerImage
        isAdult
      }
    }
  }'''

  media = '''query($id: Int) {
    Media (id: $id) {
      id
      title {
        english
        romaji
      }
      type
      format
      coverImage {
        color
        extraLarge
      }
      bannerImage
      isAdult
    }
  }'''

  entry = '''query($userIds: [Int], $mediaId: Int) {
    Page (page: 1, perPage: 50) {
      mediaList (userId_in: $userIds, mediaId: $mediaId) {
        status
        score
        progress
        user {
          id
        }
      }
    }
  }'''

  favourites = '''query($userId: Int) {
    User (id: $userId) {
      favourites {
        anime {
          n: nodes {
            title {
              english
              romaji
            }
            coverImage {
              extraLarge
            }
          }
        }
        manga {
          n: nodes {
            title {
              english
              romaji
            }
            coverImage {
              extraLarge
            }
          }
        }
        characters {
          n: nodes {
            title: name {
              english: full
            }
            coverImage: image {
              extraLarge: large
            }
          }
        }    
        staff {
          n: nodes {
            title: name {
              english: full
            }
            coverImage: image {
              extraLarge: large
            }
          }
        }
      }
    }
  }'''

  activity = '''query($userId: Int) {
    Activity (userId: $userId, type: MEDIA_LIST, sort: ID_DESC) {
      ... on ListActivity {
        status
        progress
        createdAt
        media {
          title {
            english
            romaji
          }
        }
      }
    }
  }'''

  staff = '''query ($id: Int) {
    Staff(id: $id) {
      name {
        full
      }
      image {
        large
      }
      primaryOccupations
      voiceartist: characters (sort: FAVOURITES_DESC) {
        e: edges {
          role
          n: node {
            title: name {
              english: full
            }
            image {
              extraLarge: large
            }
          }
        }
      }
      artist: staffMedia (sort: FAVOURITES_DESC) {
        e: edges {
          role: staffRole
          n: node {
            title {
              english
              romaji
            }
            image: coverImage {
              extraLarge
            }
          }
        }
      }
    }
  }'''

  searchStaff = '''query ($query: String) {
    Page (page: 1, perPage: 10) {
      staff(search: $query) {
        id
        name {
          full
        }
        primaryOccupations
      }
    }
  }'''