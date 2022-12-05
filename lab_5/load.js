import http from 'k6/http';
import { check, group, sleep } from 'k6';


export const options = {
  stages: [
    { duration: '1m', target: 100 }, // simulate ramp-up of traffic from 1 to 100 users over 3 minutes.
    { duration: '5m', target: 100 }, // stay at 100 users for 7 minutes
    { duration: '5s', target: 0 }, // ramp-down to 0 users
  ],
  thresholds: {
    'http_req_duration': ['p(99)<500'] // 99% of requests must complete below 1.5s
  },
};

const features = [
  "MedInc",
  "HouseAge",
  "AveRooms",
  "AveBedrms",
  "Population",
  "AveOccup",
  "Latitude",
  "Longitude",
]
const fixed = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0]

const randInt = (max) => Math.floor(Math.random() * max)

const generator = (cacheRate) => {
  const rand = Math.random()
  const input = rand > cacheRate
    ? features.reduce((acc, f) => {
        acc[f] = [randInt(20)]
        return acc
      }, {})
    : features.reduce((acc, f, idx) => {
        acc[f] = [fixed[idx]]
        return acc
      }, {})

//how to create list in JS, send to API

  return input

}

const NAMESPACE = 'marcusmanos'
const BASE_URL = `https://${NAMESPACE}.mids255.com`;
const CACHE_RATE = 0.9

export default () => {
  const healthRes = http.get(`${BASE_URL}/health`)
  check(healthRes, {
    'is 200': (r) => r.status === 200,
//    'status healthy': (r) => r.json('status') === 'OK',
  })

  const payload = JSON.stringify(generator(CACHE_RATE))
  //console.log(payload)
  const predictionRes = http.request('POST', `${BASE_URL}/predict`, payload)
  //console.log(predictionRes.json('predictions.0.output[0]'))
  check(predictionRes, {
    'is 200': (r) => r.status === 200,
    'is Float': (r) => parseFloat(r.json('output.0')),
  })
};



//   "MedInc": [10.0, 10.0],
//kubectl --namespace $NAMESPACE logs deployment.apps/lab4 to check the logs

//to run the script: k6 run --summary-trend-stats="min,med,avg,max,p(99)" load.js

// API output: {"output":[1.9375488146891446,1.9375488146891446]}

// to run grafana: kubectl port-forward -n prometheus svc/grafana 3000:3000