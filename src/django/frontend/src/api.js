import Vue from "vue"
import VueResource from "vue-resource"
import Axios from "axios"

Vue.use(VueResource);

const path = (...args)=> [...args].join("/")+"/"

export default function(csrftoken,url){
   if(url !== undefined){
      url = "/api"
   }
   this.url = "/api" 

   this.staticArgs = {
      credentials: "include",
      headers: {
         "X-CSRFToken": csrftoken,
         "Content-Type": "application/json"
      }
   }

   this._requestSet = (method)=>{
      let rq = (url,...args)=>{
         args = {...this.staticArgs, ...args[0]}
         return Axios({method: method, url: url,...args})
            .catch((e)=>{
               // Here i could reroute to an error page which
               // would let the user report the issue?
               console.log(`There was an error: ${e}`)
            })
      }
      return {
         rel: (url,...args)=>{
            return rq(path(this.url,url),...args)
         },
         abs: rq
      }
   }

   this.get = this._requestSet("get")
   this.post = this._requestSet("post")
   this.put = this._requestSet("put")
   this.del = this._requestSet("delete")
};
