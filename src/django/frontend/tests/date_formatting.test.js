
import {format_date} from "@/date_formatting"

let tests = [
   {input:"1999-01-1",output:"January 1999"},
   {input:"2001-04-1",output:"April 2001"},
   {input:"100-10-1",output:"October 100"},
   {input:"3000-07-1",output:"July 3000"},
   {input:"1992-12-1",output:"December 1992"},
]

tests.forEach((pair)=>{
   test(`formats ${pair.input}`,()=>{
      expect(format_date(pair.input)).toBe(pair.output)
   })
})
