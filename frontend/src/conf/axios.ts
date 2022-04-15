import axios from 'axios'
import conf from './conf'

const createBaseInstance = () =>
    axios.create({
        baseURL: conf.baseUrl,
        headers: {},
    })

const axiosInstance = createBaseInstance()

export default axiosInstance
