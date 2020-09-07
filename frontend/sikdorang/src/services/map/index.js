import loadScriptOnce from 'load-script-once'

const DAUM_KAKAO_API_JS_KEY = 'd313fa70ad00838acce4a3b5bc134b23'
const DAUM_KAKAO_MAP_LIB_URL = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${DAUM_KAKAO_API_JS_KEY}&libraries=drawing,clusterer,services&autoload=false`

class Map {
  constructor () {
    this.map = null
    Map.initialize()
  }

  async mount (elementId) {
    await Map.initialize()

    // re-use map
    if (Map.cachedMaps[elementId]) {
      this.map = Map.cachedMaps[elementId]
      const oldElement = this.map.getNode()
      const newElement = document.getElementById(elementId)
      newElement.parentNode.replaceChild(oldElement, newElement)

    // create map
    } else {
      this.map = new Map.daum.maps.Map(
        document.getElementById(elementId),
        {
          center: new Map.daum.maps.LatLng(35.65919598808177, 127.73894402702498),
          level: 13,
        },
      )
      this.map.setCopyrightPosition(Map.daum.maps.CopyrightPosition.BOTTOMRIGHT, true)
      this.map.clusters = {}
      this.map.markersWithoutCluster = []
      Map.cachedMaps[elementId] = this.map
    }
    return this
  }

  addMarkerClusters (clusterSpecs = []) {
    clusterSpecs.forEach(({ key, color, zIndex = 0, singleIconURL = null }) => {
      if (this.map.clusters[key]) return

      const cluster = this.map.clusters[key] = new Map.daum.maps.MarkerClusterer({
        map: this.map,
        averageCenter: true,
        gridSize: 30,
        minClusterSize: 2,
        minLevel: 10,
        disableClickZoom: false,
        calculator: [10, 20], // 0~9, 10~19, 20~
        styles: [
          {
            width: '30px',
            height: '30px',
            background: color,
            opacity: 0.95,
            border: '2px solid white',
            borderRadius: '100%',
            color: 'white',
            textAlign: 'center',
            lineHeight: '27px',
            fontSize: '20px',
            fontWeight: 'bold',
          },
          {
            width: '36px',
            height: '36px',
            background: color,
            opacity: 0.95,
            border: '2px solid white',
            borderRadius: '100%',
            color: 'white',
            textAlign: 'center',
            lineHeight: '33px',
            fontSize: '22px',
            fontWeight: 'bold',
          },
          {
            width: '48px',
            height: '48px',
            background: color,
            opacity: 0.95,
            border: '2px solid white',
            borderRadius: '100%',
            color: 'white',
            textAlign: 'center',
            lineHeight: '44px',
            fontSize: '25px',
            fontWeight: 'bold',
          },
        ],
      })

      cluster._icon = new Map.daum.maps.MarkerImage(
        singleIconURL,
        new Map.daum.maps.Size(15, 15),
      )

      cluster._zIndex = zIndex
    })
    return this
  }

  addMarkers (markerSpecs = []) {
    const markerSpecsWithoutClusterKey = []
    const markerSpecsByClusterKey = markerSpecs.reduce((result, spec) => {
      if (!spec.clusterKey) {
        markerSpecsWithoutClusterKey.push(spec)
        return result
      }
      if (!result[spec.clusterKey]) {
        result[spec.clusterKey] = []
      }
      result[spec.clusterKey].push(spec)
      return result
    }, {})

    markerSpecsWithoutClusterKey.forEach(({ lat, lng, title = null, onClick = null }) => {
      const marker = new Map.daum.maps.Marker({
        map: this.map,
        position: new Map.daum.maps.LatLng(lat, lng),
        title,
      })

      if (onClick) {
        Map.daum.maps.event.addListener(marker, 'click', onClick)
      }

      this.map.markersWithoutCluster.push(marker)
    })

    for (let clusterKey in markerSpecsByClusterKey) {
      const cluster = this.map.clusters[clusterKey]
      cluster.addMarkers(
        markerSpecsByClusterKey[clusterKey].map(({ lat, lng, title = null, onClick = null }) => {
          const marker = new Map.daum.maps.Marker({
            title,
            position: new Map.daum.maps.LatLng(lat, lng),
            image: cluster._icon,
            zIndex: cluster._zIndex,
          })

          if (onClick) {
            Map.daum.maps.event.addListener(marker, 'click', onClick)
          }

          return marker
        })
      )
    }
  }

  clearMarkers () {
    // remove cluster markers
    for (let k in this.map.clusters) {
      const cluster = this.map.clusters[k]
      cluster.clear()
    }

    this.map.markersWithoutCluster.forEach(marker => {
      marker.setMap(null)
    })

    this.map.markersWithoutCluster = []
  }

  setCenter ({ lat, lng, maxLevel = 8 }) {
    if (this.map.getLevel() > maxLevel) {
      this.map.setLevel(maxLevel)
    }
    this.map.panTo(
      new Map.daum.maps.LatLng(lat, lng)
    )
  }
}

Map.cachedMaps = {}
Map.daum = null
Map.initialize = function () {
  return new Promise((resolve, reject) => {
    loadScriptOnce(DAUM_KAKAO_MAP_LIB_URL, (err) => {
      if (err) return reject(err)
      Map.daum = window.daum
      Map.daum.maps.load(() => resolve())
    })
  })
}

export default Map