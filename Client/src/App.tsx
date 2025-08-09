
import Chat from './components/Chat'
import Footer16 from './components/Footer'
import Navbar from './components/Navbar'
import { Demo } from './components/Textinput'

function App() {

  return (
    <div className='bg-black'>
      <div className=''>
        <Navbar />
      </div>
      <div className='w-full'>
        <Chat />
      </div>
      <div className=' flex justify-center w-full'>
        <div className='w-2xl m-2'>
          <Demo />
        </div>
      </div>
      <div className='h-2vh'>
        <Footer16 />
      </div>
    </div>
  )
}

export default App
