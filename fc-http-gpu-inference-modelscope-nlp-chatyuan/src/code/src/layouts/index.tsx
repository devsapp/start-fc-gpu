import { Helmet, Outlet } from 'umi';

export default function Layout() {
  return (
    <div>
      <Helmet>
        <script src="/endpoint.js"></script>
      </Helmet>
      <Outlet />
    </div>
  );
}
