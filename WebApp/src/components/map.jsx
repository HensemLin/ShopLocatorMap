import { useCallback, useEffect, useState } from "react";
import { MapContainer, Marker, Popup, TileLayer, GeoJSON } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import getShop from "../services/getShop";
import { Icon } from "leaflet";
import * as turf from "@turf/turf";
import intersection from "../utils/intersection";
import { aim } from "../assets";

const Map = () => {
  const [center, setCenter] = useState([]);
  const [shops, setShops] = useState(null);
  const [intersectCircles, setIntersectCircles] = useState([]);
  const [map, setMap] = useState(null);
  const ZOOM_LEVEL = 11;
  const option = {
    steps: 64,
    units: "kilometers",
    options: {},
  };
  var circles = [];

  const LeafIcon = Icon.extend({ options: {} });

  const redIcon = new LeafIcon({
    iconUrl:
      "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png",
    shadowUrl:
      "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41],
  });

  const blueIcon = new LeafIcon({
    iconUrl:
      "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png",
    shadowUrl:
      "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41],
  });

  function DisplayPosition({ map }) {
    const [position, setPosition] = useState(() => map.getCenter());

    const onClick = useCallback(() => {
      map.setView(center, ZOOM_LEVEL);
    }, [map]);

    const onMove = useCallback(() => {
      setPosition(map.getCenter());
    }, [map]);

    useEffect(() => {
      map.on("move", onMove);
      return () => {
        map.off("move", onMove);
      };
    }, [map, onMove]);

    return (
      <div className="w-full mt-5 ml-2">
        <div className="bg-slate-100 border-slate-400 border-2 rounded-lg w-10 h-10 items-center justify-center">
          <a
            className="flex bg-transparent w-full h-full p-0 items-center justify-center cursor-pointer"
            onClick={onClick}
          >
            <img className="object-cover w-8 h-8" src={aim} />
          </a>
        </div>
      </div>
    );
  }

  useEffect(() => {
    const fetchShops = async () => {
      try {
        const shopDetails = await getShop(
          "http://localhost:8000/shop/",
          import.meta.env.VITE_APP_API_KEY
        );
        if (shopDetails) {
          setCenter([shopDetails.center.lat, shopDetails.center.lon]);
          setShops(shopDetails.shop);
        }
      } catch (error) {
        console.error("Error fetching shop details:", error);
      }
    };
    fetchShops();
  }, []);

  useEffect(() => {
    const findInterception = () => {
      if (shops != null && shops.length > 0) {
        shops.map((shop) => {
          const circle = {
            center: [shop.location.lon, shop.location.lat],
            radius: 5,
          };
          circles.push(circle);
        });
        const intersectedCircle = intersection(circles);
        setIntersectCircles(intersectedCircle, option);
      }
    };
    findInterception();
  }, [shops]);

  return (
    <div className="flex-row w-full h-fit mt-20">
      <div className="flex-col text-center w-full h-fit">
        <div className="flex w-full h-fit p-6">
          {center.length > 0 && shops.length > 0 ? (
            <div className="flex flex-col w-full h-fit">
              <MapContainer center={center} zoom={ZOOM_LEVEL} ref={setMap}>
                <TileLayer
                  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                {shops.map((shop, index) => {
                  return (
                    <div>
                      <Marker
                        key={index}
                        position={[shop.location.lat, shop.location.lon]}
                        icon={
                          intersectCircles.includes(index) ? blueIcon : redIcon
                        }
                      >
                        <Popup>
                          <div className="flex-col w-full">
                            <p className="font-bold">{shop.name}</p>
                            <span className="text">{shop.address}</span>
                            <div className="flex w-full justify-end">
                              <p className="text">{`[${shop.location.lat},${shop.location.lon}]`}</p>
                            </div>
                          </div>
                        </Popup>
                      </Marker>
                      <GeoJSON
                        data={turf.circle(
                          [shop.location.lon, shop.location.lat],
                          5,
                          option
                        )}
                        style={{
                          color: `${
                            intersectCircles.includes(index) ? "blue" : "red"
                          }`,
                          weight: 2,
                        }}
                      />
                    </div>
                  );
                })}
              </MapContainer>
              {map ? <DisplayPosition map={map} /> : null}
            </div>
          ) : (
            <div className="text-white">loading</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Map;
