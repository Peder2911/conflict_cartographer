//jest.mock("@/util/debounce")

import {mount} from "@vue/test-utils"
import flushPromises from "flush-promises"
import {Api} from "@/testutils"
import {mock_countries} from "@/mocking"

import LoadingRouter from "@/components/LoadingRouter"

function mockRouter(){
   this.path = undefined
   this.push = (path)=>{
      this.path = path
   }
}

let mock_responses = {"profile/whoami":{name:""}}

let respres=[
   {
      responses:{
         get:{
            "period/open":{
               open:false
            },
            "profile/exists":{
               profile: true 
            },
            ...mock_responses
         },
      },
      result_path: "/menu"
   },
   {
      responses:{
         get:{
            "period/open":{
               open:true
            },
            "profile/assigned":{
               countries:[]
            },
            "profile/unfulfilled":{
               countries:[]
            },
            "profile/exists":{
               profile: false 
            },
            ...mock_responses
         },
      },
      result_path: "/assign"
   },
   {
      responses:{
         get:{
            "period/open":{
               open:true
            },
            "profile/assigned":{
               countries:[mock_countries(3)]
            },
            "profile/unfulfilled":{
               countries:[mock_countries(3)]
            },
            "profile/exists":{
               profile: false 
            },
            ...mock_responses
         },
      },
      result_path: "/progress"
   },
   {
      responses:{
         get:{
            "period/open":{
               open:true
            },
            "profile/assigned":{
               countries:[mock_countries(3)]
            },
            "profile/unfulfilled":{
               countries:[]
            },
            "profile/exists":{
               profile: false 
            },
            ...mock_responses
         },
      },
      result_path: "/questionaire"
   },
   {
      responses:{
         get:{
            "period/open":{
               open:true
            },
            "profile/assigned":{
               countries:[mock_countries(3)]
            },
            "profile/unfulfilled":{
               countries:[]
            },
            "profile/exists":{
               profile: true
            },
            ...mock_responses
         },
      },
      result_path: "/status"
   },
]

test("Shows info",()=>{
   let mr = new mockRouter()
   let api = new Api({get:mock_responses})
   mount(LoadingRouter,{
      mocks:{$cookies:{get(){return false}},$router:mr,$api:api},
   })
   expect(mr.path).toMatch("/info")
})

respres.forEach((pair)=>{
   let {responses,result_path}=pair
   test(`Reaches ${result_path}`,async ()=>{
      let api = new Api(responses)
      let mr = new mockRouter()
      mount(LoadingRouter,{
         mocks:{
            $cookies:{get(){return true}},
            $api:api,
            $router: mr 
         }
      })
      await flushPromises()
      expect(mr.path).toMatch(new RegExp(result_path))
   })
})
