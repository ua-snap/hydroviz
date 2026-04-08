export const getHandleCoord = (feature: any) => {
  const { $L } = useNuxtApp()
  let firstCoord = feature.geometry.coordinates[0][0]
  return $L.latLng(firstCoord[1], firstCoord[0])
}
