import store from '@/store'
import router from '@/router'

const GENERAL_HOOK = process.env.VUE_APP_GENERAL_HOOK
const GENERAL_API_HOOK = `${GENERAL_HOOK}/api/`
const GENERAL_BLOG_API_HOOK = `${GENERAL_API_HOOK}blog/`
const GENERAL_NEWS_API_HOOK = `${GENERAL_BLOG_API_HOOK}news/`

const GENERAL_SOUND_API_HOOK = `${GENERAL_API_HOOK}sounds/`
const GAME_FOLDERS_API_LINK = `${GENERAL_SOUND_API_HOOK}folders/`

function GET_GAME_FOLDER_DETAILS_API_LINK(folder_id) {
  return `${GAME_FOLDERS_API_LINK}${folder_id}/`
}

const GAME_SOUNDS_API_LINK = `${GENERAL_SOUND_API_HOOK}sounds/`

function GET_GAME_SOUND_DETAILS_API_LINK(sound_id) {
  return `${GAME_SOUNDS_API_LINK}${sound_id}/`
}

const SOUND_REVIEWS_API_LINK = `${GENERAL_SOUND_API_HOOK}reviews/`

function GET_SOUND_REVIEW_DETAILS_API_LINK(review_id) {
  return `${SOUND_REVIEWS_API_LINK}${review_id}/`
}

const GAME_SOUND_CATEGORIES_API_LINK = `${GENERAL_SOUND_API_HOOK}categories/`

const GENERAL_ACCOUNT_HOOK = `${GENERAL_HOOK}/auth/`
const AUTH_GET_TOKEN_API = `${GENERAL_ACCOUNT_HOOK}token/`
const AUTH_REFRESH_TOKEN_API = `${GENERAL_ACCOUNT_HOOK}token/refresh/`
const AUTH_BLACKLIST_TOKEN_API = `${GENERAL_ACCOUNT_HOOK}token/blacklist/`
const AUTH_SIGNUP_API_LINK = `${GENERAL_ACCOUNT_HOOK}signup/`

async function fetch_api_json(
  link,
  method = 'GET',
  body_data = null,
  init = null,
) {
  if (!init) {
    init = {
      method: method,
      headers: {
        'Content-Type': 'application/json',
        Authorization: await store.dispatch('getAuthHeader'),
      },
      mode: 'cors',
    }
    if (body_data) {
      init.body = JSON.stringify(body_data)
    }
  }
  let res = await fetch(link, init)
  if (res.status === 401) {
    // Not authenticated
    window.location.href = router.resolve({ name: 'Logout' }).href
    window.location.reload()
    return null
  } else if (res.status === 404 && process.env.VUE_APP_REDIRECT_ON_ERROR) {
    // Page not found
    window.location.href = router.resolve({ name: 'Page404' }).href
    window.location.reload()
  } else if (res.status === 403) {
    // Doesn't have permission
    return null
  }
  return res
}

async function fetch_auth_json(
  link,
  method = 'POST',
  body_data = null,
  init = null,
) {
  if (!init) {
    init = {
      method: method,
      headers: {
        'Content-Type': 'application/json',
      },
      mode: 'cors',
    }
    if (body_data) {
      init.body = JSON.stringify(body_data)
    }
  }
  return await fetch(link, init)
}

export {
  fetch_api_json,
  fetch_auth_json,
  GENERAL_NEWS_API_HOOK,
  AUTH_GET_TOKEN_API,
  AUTH_BLACKLIST_TOKEN_API,
  AUTH_REFRESH_TOKEN_API,
  AUTH_SIGNUP_API_LINK,
  GAME_FOLDERS_API_LINK,
  GET_GAME_FOLDER_DETAILS_API_LINK,
  GAME_SOUNDS_API_LINK,
  GET_GAME_SOUND_DETAILS_API_LINK,
  SOUND_REVIEWS_API_LINK,
  GET_SOUND_REVIEW_DETAILS_API_LINK,
  GAME_SOUND_CATEGORIES_API_LINK,
}
