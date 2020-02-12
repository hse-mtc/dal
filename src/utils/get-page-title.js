import defaultSettings from '@/settings'

const title = defaultSettings.title || 'ВУЦ ВШЭ'

export default function getPageTitle(pageTitle) {
  if (pageTitle) {
    return `${pageTitle} - ${title}`
  }
  return `${title}`
}
