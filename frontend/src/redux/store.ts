import { applyMiddleware, combineReducers, createStore } from 'redux'
import thunk from 'redux-thunk'
import themeReducer from '../features/theme/themeSlice'
import indicesReducer from '../features/Indices/indicesSlice'
import { persistStore } from 'redux-persist'
import notificationReducer from '../features/Notification/notificationSlice'
import indexSearchReducer from '../features/Indices/Search/indexSearchSlice'
import { composeWithDevTools } from 'redux-devtools-extension'

// Redux Devtools
const composeEnhancers = composeWithDevTools({})

const store = createStore(
    combineReducers({
        indices: indicesReducer,
        theme: themeReducer,
        notification: notificationReducer,
        indexSearch: indexSearchReducer,
    }),
    composeEnhancers(applyMiddleware(thunk))
)

export default store
export const persistor = persistStore(store)
export type AppStore = typeof store
export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
