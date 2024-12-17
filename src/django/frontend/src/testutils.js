
function Api(endpoints){
   this.calls = []

   this.typeGetterFactory = (type)=>{
      return ()=>{
         return this.calls.filter((c)=>{
            return c.type == type 
         })
      }
   }

   this.mockResponseFactory = (type) => {
      return async (path, args)=>{
         this.calls.push({
            path: path,
            type: type,
            args: args,
            response: endpoints[path]
         })

         return Promise.resolve({data: endpoints[type][path]})
      }
   }

   this.get = {
      abs: this.mockResponseFactory("get"),
      rel: this.mockResponseFactory("get"),
   }
   this.gets = this.typeGetterFactory("get")

   this.post = {
      abs: this.mockResponseFactory("post"),
      rel: this.mockResponseFactory("post"),
   }
   this.posts = this.typeGetterFactory("post")

   this.put = {
      abs: this.mockResponseFactory("put"),
      rel: this.mockResponseFactory("put"),
   }
   this.puts = this.typeGetterFactory("put")

   this.del = {
      abs: this.mockResponseFactory("delete"),
      rel: this.mockResponseFactory("delete"),
   }
   this.dels = this.typeGetterFactory("delete")
}


module.exports.Api = Api
