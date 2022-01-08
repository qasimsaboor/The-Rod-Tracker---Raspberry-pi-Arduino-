

async function updateStatus() {

  updateCurrentColorOpenCV()// Update current color based on Open CV
  updateMotorStatus()// Update motor status

}

function recordImage() {
  try {
    console.log('record image')
    return axios.post('/record_frame')
  } catch (e) {
    console.log('Error getting the status', e)
    updateStatus('Error getting the status')
  }
}
/**
 * Update the current color based on OpenCV
 */
 async function updateCurrentColorOpenCV() {
  try {
    // Request color from server
    const requestResult = await requestColorFromOpenCV()
    // Get the HTML element where the status is displayed
    const green_open_cv = document.getElementById('green_open_cv')
    green_open_cv.innerHTML = requestResult.data[0]
    const cyan_open_cv = document.getElementById('cyan_open_cv')
    cyan_open_cv.innerHTML = requestResult.data[1]
    const yellow_open_cv = document.getElementById('yellow_open_cv')
    yellow_open_cv.innerHTML = requestResult.data[2]
    //console.log(yellow_open_cv.innerHTML)

  } catch (e) {
    console.log('Error getting the color based on OpenCV', e)
    updateStatus('Error getting the color based on OpenCV')
  }
}


async function updateFrame() {
  try {
    // Make request to server
    setTimeout(function() {
      img=document.getElementById('background')
      img.src = img.src.split("?")[0] + "?" + new Date().getTime()
      console.log('frame update');
    }, 100);

  } catch (e) {
    console.log('Error getting the status', e)
    updateStatus('Error getting the status')
  }
}

/**
async function updateFrame() {

      img=document.getElementById('background')
      img.src = img.src.split("?")[0] + "?" + new Date().getTime()
}
*/
/**
 * Function to request the server to update the current color based on OpenCV
 */
 function requestColorFromOpenCV () {
  try {
    // Make request to server
    return axios.get('/get_color_from_opencv')
  } catch (e) {
    console.log('Error getting the status', e)
    updateStatus('Error getting the status')
  }
}

 function requestStartMotor () {
  try {
    // Make request to server
    return axios.post('/start_motor')
  }catch (e) {
    console.log('Error starting motor', e)
    updateStatus('Error starting motor')
  }
}

var flag_cyan = false;
let i_g = 0;

function startAutoUpdate(){
    //flag_cyan = false; //end auto_update to avoid conflict
    i_g = 0;
    flag_cyan = !flag_cyan;
    console.log('flag_update:',flag_cyan)
    updateStatus();
    if (flag_cyan == true){
      axios.post('/set_random');
      AutoCyan();
      console.log('called_AutoUpdate', flag_cyan)
    }
}

function startAutoCyan(){
  i_g = 0;
  flag_cyan = !flag_cyan;
  console.log('flag_update:',flag_cyan)
  updateStatus();
  if (flag_cyan == true){
    axios.post('/set_cyan');
    AutoCyan();
    console.log('called_AutoUpdate', flag_cyan)
  }
}


var requestMotorResultglobal

async function AutoCyan() {
  try{
    if (flag_cyan == true){
      requestMotorResultglobal = await axios.get('/get_motor_status')
      console.log('motor status:',requestMotorResultglobal)
      i_g++;
      updateFrame() ; //image recording happens within python!
      updateStatus();
      if (i_g > 1) {

        if (requestMotorResultglobal.data == 'stopped'){console.log('interrupted');flag_cyan=false;}
        if (requestMotorResultglobal.data == 'finished'){console.log('recognized stop');flag_cyan=false;}

      }
      setTimeout(AutoCyan, 100);}

    else {requestStopMotor ();
        console.log('stopped_motor');}
    }
    catch(e) {
      console.log(e);
  }}

function requestStopMotor () {
  try {
    // Make request to server
    return axios.post('/stop_motor')
  }catch (e) {
    console.log('Error stopping motor', e)
    updateStatus('Error stopping motor')
  }
}

async function updateMotorStatus() {
  try {
    // Request color from server
    const requestMotorResult = await requestMotorStatus()
    // Get the HTML element where the status is displayed
    const motor_outp = document.getElementById('motor_status')
    //motor_outp.innerHTML = requestMotorResult.data
    motor_outp.innerHTML =requestMotorResultglobal.data

  }catch (e) {
    console.log('Error stopping motor', e)
    updateStatus('Error stopping motor')
  }
}

function requestMotorStatus() {
  try {
    // Make request to server
    return axios.get('/get_motor_status')
  } catch (e) {
    console.log('Error getting the status', e)
    updateStatus('Error getting the status')
  }
}





/**
 * Update the current color based on distance sensor
 */
 function updateDistance() {
  // Get the HTML element where the status is displayed
  // ...
}


/**
 * Function to request the server to get the distance from
 * the rod to the ultrasonic sensor
 */
function requestDistance () {
  //...
}


/**
 * Update the current color based on distance sensor
 */
 function updateCurrentColorDistance() {
  // Get the HTML element where the status is displayed
  // ...
}


/**
 * Function to request the server to get the color based
 * on distance only
 */
function requestColorFromDistance () {
  //...
}

