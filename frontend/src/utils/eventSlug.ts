/**
 * Convert an event object to a URL-friendly slug: "city_year".
 * This is a frontend-only convention — the backend has no notion of slugs.
 * Used in query params: /event?event=homestead_2024
 */
export const toSlug = (evt: { name: string; date: string }): string => {
    const name = evt.name.toLowerCase().replace(/ /g, '-')
    return `${name}_${new Date(evt.date).getFullYear()}`
}
