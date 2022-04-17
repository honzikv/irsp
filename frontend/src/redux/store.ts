import { applyMiddleware, combineReducers, createStore } from 'redux'
import thunk from 'redux-thunk'
import themeReducer from '../features/theme/themeSlice'
import indicesReducer from '../features/Indices/indicesSlice'
import { persistStore } from 'redux-persist'
import notificationReducer from '../features/Notification/notificationSlice'

const store = createStore(
    combineReducers({ indices: indicesReducer, theme: themeReducer, notification: notificationReducer }),
    applyMiddleware(thunk)
)

export default store
export const persistor = persistStore(store)
export type AppStore = typeof store
export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
