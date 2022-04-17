import { AlertColor } from '@mui/material'
import { createSlice } from '@reduxjs/toolkit'

export interface NotificationState {
    message?: string
    severity: AlertColor
    autohideSecs?: number
}

const initialState = {
    message: undefined,
    severity: 'info',
    autohideSecs: undefined
}

const notificationSlice = createSlice({
    name: 'notification',
    initialState,
    reducers: {
        showNotification: (state, action) => ({
            ...state,
            message: action.payload.message,
            severity: action.payload.severity,
            autohideSecs: action.payload.autohideSecs,
        }),
        // consumes the message so it is not displayed after the page gets refreshed
        consumeNotification: (state) => ({
            ...initialState,
        }),
    },
})

const notificationReducer = notificationSlice.reducer
export const { showNotification, consumeNotification } =
    notificationSlice.actions
export default notificationReducer
