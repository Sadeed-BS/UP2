
import { Demo } from './components/Textinput'

function App() {

  return (
    <div className='h-screen w-full relative bg-black'>
      <div className='navbar'></div>
      <div className='w-full'></div>
      <div className='absolute inset-x-0 bottom-0 flex justify-center w-full'>
        <div className='w-2xl'>
          <Demo />
        </div>
      </div>
    </div>
  )
}

export default App
