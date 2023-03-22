import * as timeDelta from 'time-delta'
import ruLocale from 'time-delta/locales/ru'

timeDelta.addLocale(ruLocale)

function format_url_with_get_params(base_url, params) {
  let url = new URL(base_url, location)
  if (!params) {
    return url
  }
  Object.entries(params).forEach(([key, value]) => {
    if (value !== '' && value !== null && value !== [] && value !== undefined) {
      if (Array.isArray(value)) {
        value.forEach((value) =>
          url.searchParams.append(key, value.toString().trim()),
        )
      } else {
        url.searchParams.set(key, value.toString().trim())
      }
    }
  })
  return url.href
}

function filter_body_data(body_data, values_to_skip = [null, undefined, '']) {
  body_data = Object.fromEntries(
    Object.entries(body_data).filter(([, v]) => !values_to_skip.includes(v)),
  )
  return body_data
}

function* chunks(arr, n) {
  for (let i = 0; i < arr.length; i += n) {
    yield { count: i, items: arr.slice(i, i + n) }
  }
}

function groupBy(xs, key) {
  return xs.reduce(function (rv, x) {
    ;(rv[x[key]] = rv[x[key]] || []).push(x)
    return rv
  }, {})
}

function format_russian_datetime(datetime_iso_string, date_only = false) {
  let options = {
    year: 'numeric',
    month: 'long',
    day: '2-digit',
  }
  if (!date_only) {
    options = { ...options, hour: '2-digit', minute: '2-digit' }
  }
  return new Date(Date.parse(datetime_iso_string)).toLocaleString('ru', options)
}

function format_noun_for_numeral(value, words) {
  value = Math.abs(value) % 100
  let num = value % 10
  if (value > 10 && value < 20) return words[2]
  if (num > 1 && num < 5) return words[1]
  if (num === 1) return words[0]
  return words[2]
}

function get_timedelta(start, end) {
  const instance = timeDelta.create({
    locale: 'ru',
  })
  const date1 = new Date(start)
  const date2 = new Date(end)
  return instance.format(date1, date2)
}

export {
  format_url_with_get_params,
  filter_body_data,
  chunks,
  groupBy,
  format_russian_datetime,
  get_timedelta,
  format_noun_for_numeral,
}
