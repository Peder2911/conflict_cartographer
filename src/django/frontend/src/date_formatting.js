
const months=[
   "January",
   "February",
   "March",
   "April",
   "May",
   "June",
   "July",
   "August",
   "September",
   "October",
   "November",
   "December",
]

const short_months=[
   "Jan",
   "Feb",
   "Mar",
   "Apr",
   "May",
   "Jun",
   "Jul",
   "Aug",
   "Sep",
   "Oct",
   "Nov",
   "Dec",
]

export function format_date(date,options){
   options = options? options:{}
   if(typeof(date)==="string"){
      date = new Date(date)
   }
   let lookup = options.short? short_months:months
   let pf = options.short? ".":""
   return `${lookup[date.getMonth()]}${pf} ${date.getFullYear()}`
}
