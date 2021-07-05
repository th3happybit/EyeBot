export const WEB_SOCKET_BASE_URL = 'ws://raspberrypi:8000';
// export const WEB_SOCKET_BASE_URL = 'ws://localhost:8000';

export const JOYSTICK_WSS_URL = WEB_SOCKET_BASE_URL + '/joystick_ws';
export const CAM_WSS_URL = WEB_SOCKET_BASE_URL + '/camera_ws';
export const OBJECTS_WSS_URL = WEB_SOCKET_BASE_URL + '/objects_ws';

// export const CAM_SERVER = 'http://raspberrypi:8082';
// export const CAM_SERVER = 'https://www.youtube.com/embed/jgnkQ2f84og';
export const CAM_SERVER = 'http://192.168.43.10:5000';

export const API_URL = 'http://raspberrypi:8000/';

export const IFRAME_RATIO = {
    height: 480,
    width: 640
};
