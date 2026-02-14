import {router} from "./index";

router.beforeEach((to, _, next) => {
    // Устанавливаем заголовок страницы из мета-данных маршрута
    const title = to.meta.title;
    if (title) {
        document.title = title as string;
    } else {
        // Если заголовок не задан, используем дефолтное значение
        document.title = "Keystone Tracker";
    }
    next();
});